/* Minimal, dependency-free Markdown renderer tuned for this course. */
(function (g) {
  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function inline(s) {
    return s
      .replace(/`([^`]+)`/g, function (m, c) { return "<code>" + esc(c) + "</code>"; })
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[\s(])\*([^*\n]+)\*/g, "$1<em>$2</em>")
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  }
  function render(md) {
    var lines = md.replace(/\r/g, "").split("\n");
    var out = [], i = 0;
    function flushList(tag, items) {
      out.push("<" + tag + ">" + items.map(function (x) { return "<li>" + inline(x) + "</li>"; }).join("") + "</" + tag + ">");
    }
    while (i < lines.length) {
      var L = lines[i];
      // fenced code
      if (/^```/.test(L)) {
        var buf = [];
        i++;
        while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
        i++;
        out.push("<pre><code>" + esc(buf.join("\n")) + "</code></pre>");
        continue;
      }
      // callouts  :::edge Title   /   :::answer Title   /   :::exercise Title
      var cal = L.match(/^:::(edge|trap|ship|drill|answer|exercise)\s*(.*)$/);
      if (cal) {
        var body = [];
        i++;
        while (i < lines.length && !/^:::$/.test(lines[i])) { body.push(lines[i]); i++; }
        i++;
        if (cal[1] === "answer") {
          out.push('<details class="answer"><summary>' + esc(cal[2] || "Show solution") + '</summary><div class="abody">' +
            render(body.join("\n")) + "</div></details>");
        } else if (cal[1] === "exercise") {
          out.push('<div class="ex"><h3>' + esc(cal[2] || "Exercise") + "</h3>" +
            render(body.join("\n")) + "</div>");
        } else {
          out.push('<div class="callout ' + cal[1] + '"><div class="ctitle">' + esc(cal[2] || cal[1]) + "</div>" + render(body.join("\n")) + "</div>");
        }
        continue;
      }
      // orphaned ::: terminator - skip it rather than emitting stray text
      if (/^:::\s*$/.test(L)) { i++; continue; }
      // day plan  @@ Day 1 | text
      if (/^@@\s/.test(L)) {
        var rows = [];
        while (i < lines.length && /^@@\s/.test(lines[i])) {
          var p = lines[i].slice(3).split("|");
          rows.push("<div class='dayrow'><b>" + inline(p[0].trim()) + "</b><div>" + inline(p.slice(1).join("|").trim()) + "</div></div>");
          i++;
        }
        out.push("<div class='dayplan'>" + rows.join("") + "</div>");
        continue;
      }
      // cards  ++ Title :: body
      if (/^\+\+\s/.test(L)) {
        var cs = [];
        while (i < lines.length && /^\+\+\s/.test(lines[i])) {
          var q = lines[i].slice(3).split("::");
          cs.push("<div class='card'><h5>" + inline(q[0].trim()) + "</h5><p>" + inline(q.slice(1).join("::").trim()) + "</p></div>");
          i++;
        }
        out.push("<div class='cards'>" + cs.join("") + "</div>");
        continue;
      }
      // table
      if (/^\|/.test(L) && i + 1 < lines.length && /^\|[\s:\-|]+\|$/.test(lines[i + 1].trim())) {
        var head = L.split("|").slice(1, -1).map(function (x) { return "<th>" + inline(x.trim()) + "</th>"; }).join("");
        i += 2;
        var body2 = [];
        while (i < lines.length && /^\|/.test(lines[i])) {
          body2.push("<tr>" + lines[i].split("|").slice(1, -1).map(function (x) { return "<td>" + inline(x.trim()) + "</td>"; }).join("") + "</tr>");
          i++;
        }
        out.push("<table><thead><tr>" + head + "</tr></thead><tbody>" + body2.join("") + "</tbody></table>");
        continue;
      }
      // heading
      var h = L.match(/^(#{1,4})\s+(.*)$/);
      if (h) { out.push("<h" + h[1].length + ">" + inline(h[2]) + "</h" + h[1].length + ">"); i++; continue; }
      if (/^(---|___)\s*$/.test(L)) { out.push("<hr/>"); i++; continue; }
      // blockquote
      if (/^>\s?/.test(L)) {
        var bq = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) { bq.push(lines[i].replace(/^>\s?/, "")); i++; }
        out.push("<blockquote>" + render(bq.join("\n")) + "</blockquote>");
        continue;
      }
      // ul
      if (/^[-*]\s+/.test(L)) {
        var ul = [];
        while (i < lines.length && /^[-*]\s+/.test(lines[i])) { ul.push(lines[i].replace(/^[-*]\s+/, "")); i++; }
        flushList("ul", ul); continue;
      }
      // ol
      if (/^\d+\.\s+/.test(L)) {
        var ol = [];
        while (i < lines.length && /^\d+\.\s+/.test(lines[i])) { ol.push(lines[i].replace(/^\d+\.\s+/, "")); i++; }
        flushList("ol", ol); continue;
      }
      if (L.trim() === "") { i++; continue; }
      // paragraph
      var par = [];
      while (i < lines.length && lines[i].trim() !== "" && !/^(#{1,4}\s|[-*]\s|\d+\.\s|>|\||```|:::|@@\s|\+\+\s)/.test(lines[i])) { par.push(lines[i]); i++; }
      // Safety net: if nothing was consumed, advance anyway so the renderer
      // can never stall on a line that matches a block-start but has no handler.
      if (!par.length) { i++; continue; }
      out.push("<p>" + inline(par.join(" ")) + "</p>");
    }
    return out.join("\n");
  }
  g.MD = { render: render };
})(window);
