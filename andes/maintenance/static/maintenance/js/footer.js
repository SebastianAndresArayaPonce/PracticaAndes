$(document).ready( function () {
  var pdfInfo = {};
  var x = document.location.search.substring(1).split('&');
  for (var i in x) { var z = x[i].split('=',2); pdfInfo[z[0]] = unescape(z[1]); }
  var page = pdfInfo.page || 1;
  var topage = pdfInfo.topage || 1;
  $("#gl-footer-page").html("<b>" + page + "</b>");
  $("#gl-footer-topage").html("<b>" + topage + "</b>");
});
