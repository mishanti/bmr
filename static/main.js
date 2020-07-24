$(document).ready(function(){
var movies=[];

function loadMovies(){
  $.getJSON('/movies', function(data, status, xhr){
    for (var i = 0; i < data.length; i++ ) {
          movies.push(data[i].name);
      }
});
};

loadMovies();

$('#film_name1').autocomplete({
  source: movies,
  });
$('#film_name2').autocomplete({
  source: movies,
  });
$('#film_name3').autocomplete({
  source: movies,
  });
});
