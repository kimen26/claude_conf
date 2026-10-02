#!/usr/bin/env node
/**
 * PreToolUse hook : SQL destructive operations guard
 *
 * Matcher hooks.json : Bash|PowerShell. Bloque (exit 2 = abort + message) si le SQL réel d'une
 * commande contient DROP (TABLE, SCHEMA, DATABASE, VIEW, FUNCTION, PROCEDURE, STREAMLIT, STAGE,
 * USER, ROLE, WAREHOUSE, TASK, PIPE), TRUNCATE, DELETE FROM sans WHERE, UPDATE sans WHERE
 * (WHERE dans la MÊME instruction, découpe sur « ; ») → évite les accidents Snowflake.
 * SQL réel = snow sql -q / -f / stdin (heredoc, here-string, < fichier, tube), python x.sql,
 * python -c "..." et python - <<EOF (le code est lu comme du texte : un DROP cité dans une
 * chaîne python -c est donc bloqué aussi, seul bruit assumé).
 *
 * Les requêtes SELECT, INSERT, UPDATE (avec WHERE) passent librement.
 *
 * LIMITE ASSUMÉE : CREATE OR REPLACE et REVOKE ne sont PAS bloqués. Le garde ne sait pas si
 * l'objet existe déjà ; bloquer serait du bruit à chaque dev. Ces deux ordres relèvent de la
 * confirmation demandée à Yann par la règle du projet, pas de ce hook. Une requête construite
 * dynamiquement (variable, f-string, fichier généré à l'exécution) échappe aussi au garde.
 *
 * Lecture stdin ASYNCHRONE : process.stdin.read() synchrone renvoyait null
 * avant l'arrivée des données → le hook laissait tout passer (bug 2026-09-03).
 */

let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (d) => (raw += d));
process.stdin.on("end", () => {
  let input = {};
  try {
    input = JSON.parse(raw || "{}");
  } catch (_) {
    process.exit(0);
  }

  const toolName = input.tool_name || "";
  const toolInput = input.tool_input || {};

  const SHELL_TOOLS = ["Bash", "bash", "PowerShell", "run_in_terminal"];
  if (!SHELL_TOOLS.includes(toolName)) process.exit(0);

  const cmd =
    typeof toolInput === "string"
      ? toolInput
      : toolInput.command || toolInput.cmd || "";
  if (!cmd) process.exit(0);

  let reason = "";
  for (const sql of sqlReel(cmd, input.cwd)) {
    reason = jugerSql(sql);
    if (reason) break;
  }

  if (reason) {
    console.error(
      `\n🛑 SQL GUARD : Opération destructive détectée : ${reason}\n` +
        `   Commande : ${cmd.substring(0, 120)}${cmd.length > 120 ? "…" : ""}\n\n` +
        `   Demande à Yann une confirmation explicite dans le chat ;\n` +
        `   il exécute lui-même.\n`
    );
    process.exit(2);
  }
  process.exit(0);
});

/** Enlève les guillemets d'un argument shell et les échappements \" d'une chaîne double. */
function deguillemeter(s) {
  if (s.length >= 2 && (s[0] === '"' || s[0] === "'") && s[s.length - 1] === s[0]) {
    const inner = s.slice(1, -1);
    return s[0] === '"' ? inner.replace(/\\(["\\])/g, "$1") : inner;
  }
  return s;
}

function lireFichier(chemin, cwd) {
  try {
    return require("fs").readFileSync(
      require("path").resolve(cwd || process.cwd(), chemin),
      "utf8"
    );
  } catch (_) {
    return "";
  }
}

/**
 * Ne rend que le SQL réel d'une commande shell :
 *  - snow sql -q "..." / --query "..."  (la chaîne)
 *  - snow sql -f x.sql / --filename x.sql  (le contenu du fichier)
 *  - snow sql -i : corps de heredoc, here-string, < fichier, texte ou fichier envoyé par un tube
 *  - python ... x.sql  (le contenu du fichier cité)
 *  - python -c "..." et corps de heredoc passé à python
 * git commit, grep, echo, cat, sed, rg, Select-String... : rien, donc jamais bloqués.
 */
function sqlReel(cmd, cwd) {
  const out = [];
  const arg = String.raw`("(?:\\.|[^"\\])*"|'[^']*'|[^\s"']+)`;
  // L'invocation se cherche hors du texte : un message de commit (heredoc ou -m "...") qui
  // cite « snow sql » ou « python » n'est pas une exécution (faux positif réel du 2026-10-02).
  // Une chaîne entre guillemets qui EST l'exécutable ("…/python.exe", "snow") reste visible.
  const squelette = sansHeredoc(cmd).replace(/"(?:\\.|[^"\\])*"|'[^']*'/g,
    (m) => (/\b(?:python[\d.]*|snow)(?:\.exe)?["']$/i.test(m) ? m : '""'));
  const surSnow = /\bsnow(?:\.exe)?["']?\s+sql\b/i.test(squelette);
  const surPython = /\bpython[\d.]*(?:\.exe)?["']?\s/i.test(squelette);
  if (surSnow) {
    for (const m of cmd.matchAll(new RegExp(String.raw`(?:^|\s)(?:-q|--query)(?:\s+|=)` + arg, "g"))) {
      out.push(deguillemeter(m[1]));
    }
    for (const m of cmd.matchAll(new RegExp(String.raw`(?:^|\s)(?:-f|--filename)(?:\s+|=)` + arg, "g"))) {
      out.push(lireFichier(deguillemeter(m[1]), cwd));
    }
  }
  if (surSnow) {
    // snow sql lit aussi son SQL sur l'entrée standard : heredoc, here-string PowerShell,
    // redirection < fichier, ou texte envoyé par un tube (echo/printf/cat/type/Get-Content).
    out.push(...corpsHeredoc(cmd));
    for (const m of cmd.matchAll(new RegExp(String.raw`(?:^|\s)<(?!<)\s*` + arg, "g"))) {
      out.push(lireFichier(deguillemeter(m[1]), cwd));
    }
    const tube = cmd.match(/^([\s\S]*?)\|\s*snow(?:\.exe)?\s+sql\b/i);
    if (tube) {
      for (const m of tube[1].matchAll(/"(?:\\.|[^"\\])*"|'[^']*'/g)) out.push(deguillemeter(m[0]));
      for (const m of tube[1].matchAll(new RegExp(String.raw`(?:^|[\s;(])(?:cat|type|Get-Content|gc)\s+(?:-Raw\s+)?` + arg, "gi"))) {
        out.push(lireFichier(deguillemeter(m[1]), cwd));
      }
    }
  }
  if (surPython) {
    for (const m of cmd.matchAll(/(?:^|\s)["']?([^\s"']+\.sql)["']?(?=\s|$)/gi)) {
      out.push(lireFichier(m[1], cwd));
    }
    // python -c "..." et python - <<EOF ... EOF : le code est analysé comme du texte SQL.
    for (const m of cmd.matchAll(new RegExp(String.raw`(?:^|\s)-c\s+` + arg, "g"))) {
      out.push(deguillemeter(m[1]));
    }
    out.push(...corpsHeredoc(cmd));
  }
  return out;
}

/** La commande sans le corps de ses heredocs ni de ses here-strings PowerShell. */
function sansHeredoc(cmd) {
  return cmd
    .replace(/<<-?\s*["']?(\w+)["']?[^\n]*\r?\n[\s\S]*?\r?\n\s*\1(?=\s|$)/g, "<<HEREDOC")
    .replace(/@(["'])\s*\r?\n[\s\S]*?\r?\n\s*\1@/g, "@''@");
}

/** Corps des heredocs (<<EOF ... EOF, <<'EOF', <<-EOF) et here-strings PowerShell (@' ... '@). */
function corpsHeredoc(cmd) {
  const out = [];
  for (const m of cmd.matchAll(/<<-?\s*["']?(\w+)["']?[^\n]*\r?\n([\s\S]*?)\r?\n\s*\1(?=\s|$)/g)) out.push(m[2]);
  for (const m of cmd.matchAll(/@(["'])\s*\r?\n([\s\S]*?)\r?\n\s*\1@/g)) out.push(m[2]);
  return out;
}

/** Une raison de blocage (chaîne) ou "". Le WHERE doit être dans la MÊME instruction (découpe sur ;). */
function jugerSql(sql) {
  const propre = sql.replace(/\/\*[\s\S]*?\*\//g, " ").replace(/--[^\n]*/g, " ");
  for (const brut of propre.split(";")) {
    const st = brut.toUpperCase();
    if (/\bDROP\s+(TABLE|SCHEMA|DATABASE|VIEW|FUNCTION|PROCEDURE|STREAMLIT|STAGE|USER|ROLE|WAREHOUSE|TASK|PIPE)\b/.test(st))
      return "DROP (suppression définitive d'un objet Snowflake)";
    if (/\bTRUNCATE\b/.test(st)) return "TRUNCATE (vidage complet d'une table)";
    if (/\bDELETE\s+FROM\b/.test(st) && !/\bWHERE\b/.test(st))
      return "DELETE FROM sans clause WHERE (suppression totale)";
    if (/^\s*UPDATE\b/.test(st) && !/\bWHERE\b/.test(st))
      return "UPDATE sans clause WHERE (modification de toutes les lignes)";
  }
  return "";
}
