(function () {
  // Copy buttons on entry pages
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var el = document.getElementById(btn.getAttribute("data-copy"));
      if (!el || !navigator.clipboard) return;
      var label = btn.textContent;
      navigator.clipboard.writeText(el.textContent.trim()).then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = label; }, 1600);
      });
    });
  });


  // Filter the classification tree on the home page
  var input = document.getElementById("q");
  if (!input) return;
  var count = document.getElementById("count");
  var initial = count.textContent;
  var items = Array.prototype.slice.call(document.querySelectorAll(".classification .tree li"));
  var branches = document.querySelectorAll(".classification .branch");

  function apply() {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    items.forEach(function (li) { li.classList.remove("hidden", "match"); });
    if (q) {
      // bottom-up so a parent stays visible when any descendant matches
      items.slice().reverse().forEach(function (li) {
        var hit = li.getAttribute("data-names").indexOf(q) !== -1;
        var childVisible = li.querySelector(":scope > ul > li:not(.hidden)");
        if (hit) li.classList.add("match");
        if (!hit && !childVisible) li.classList.add("hidden");
      });
      shown = items.filter(function (li) { return li.classList.contains("match"); }).length;
    }
    branches.forEach(function (b) {
      b.classList.toggle("empty", !!q && !b.querySelector(".tree li:not(.hidden)"));
    });
    count.textContent = q ? (shown ? shown + (shown === 1 ? " match" : " matches") : "No terms match “" + input.value.trim() + "”. Try a synonym or a shorter word.") : initial;
  }
  input.addEventListener("input", apply);
  var param = new URLSearchParams(location.search).get("q");
  if (param) { input.value = param; apply(); }
})();
