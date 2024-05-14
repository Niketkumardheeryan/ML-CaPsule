// Replace 'YOUR_API_KEY' below with your API key retrieved from https://www.themoviedb.org
var myAPI = '5df4ce8a2d253b69dc3e44ab02371168'  // global string to be consistent with future usages elsewhere
$(function() {
  $('#movie_list').css('display','none');
  $('#autoComplete').blur(function() {
    $('#movie_list').css('display','none');
  });
  // Button will be disabled until we type something inside the input field
  const source = document.getElementById('autoComplete');
  const inputHandler = function(e) {
    $('#movie_list').css('display','block');
    if(e.target.value==""){
      $('.movie-button').attr('disabled', true);
    }
    else{
      $('.movie-button').attr('disabled', false);
    }
  }
  source.addEventListener('input', inputHandler);

  $('.fa-arrow-up').click(function(){
    $('html, body').animate({scrollTop:0}, 'slow');
  });

  $('.app-title').click(function(){
    window.location.href = '/';
  })

  $('.movie-button').on('click',function(){
    var my_api_key = myAPI;
    var title = $('.movie').val();
    $('#movie_list').css('display','none');
    if (title=="") {
      $('.results').css('display','none');
      $('.fail').css('display','block');
    }

    if (($('.fail').text() && ($('.footer').css('position') == 'absolute'))) {
      $('.footer').css('position', 'fixed');
    }

    else{
      load_details(my_api_key,title,true);
    }
  });
});

// will be invoked when clicking on the recommended movie cards
function recommendcard(id){
  $("#loader").fadeIn();
  var my_api_key = myAPI;
  // var title = e.getAttribute('title'); 
  load_details(my_api_key,id,false);
}


// get the details of the movie from the API (based on the name of the movie)
function load_details(my_api_key,search,isQuerySearch){
  if(isQuerySearch) {
    url = 'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+search;
  }
  else {
    url = 'https://api.themoviedb.org/3/movie/' + search + '?api_key='+my_api_key;
  }
  $.ajax({
    type: 'GET',
    url:url,
    async: false,
    success: function(movie){
      if(!isQuerySearch) {
        $("#loader").fadeIn();
        $('.fail').css('display','none');
        $('.results').delay(1000).css('display','block');
        var movie_id = movie.id;
        var movie_title = movie.title;
        var movie_title_org = movie.original_title;
        get_movie_details(movie_id,my_api_key,movie_title,movie_title_org);
      }
      else if(movie.results.length<1){
        $('.fail').css('display','block');
        $('.results').css('display','none');
        $("#loader").delay(500).fadeOut();
      }
      else if(movie.results.length==1) {
        $("#loader").fadeIn();
        $('.fail').css('display','none');
        $('.results').delay(1000).css('display','block');
        var movie_id = movie.results[0].id;
        var movie_title = movie.results[0].title;
        var movie_title_org = movie.results[0].original_title;
        get_movie_details(movie_id,my_api_key,movie_title,movie_title_org);
      }
      else{
        $("#loader").fadeIn();
        $('.fail').css('display','none');
        $('.results').delay(1000).css('display','block');

        details = {
          'movies_list': movie.results
        }

        $.ajax({
          type:'POST',
          data:JSON.stringify(details),
          beforeSend: function() {
            $("#loader").fadeIn();
          },
          url:"/populate-matches",
          dataType: 'html',
          complete: function(){
            $("#loader").delay(1000).fadeOut();
          },
          success: function(response) {
            $('.results').delay(2000).html(response);
            $('#autoComplete').val('');
            $('.footer').css('position','relative');
            $('.social').css('padding-bottom','15px');
            $('.social').css('margin-bottom','0px');
            $(window).scrollTop(0);
          }
        });

      }
    },
    error: function(error){
      alert('Invalid Request - '+error);
      $("#loader").delay(500).fadeOut();
    },
  });
}

// get all the details of the movie using the movie id.
function get_movie_details(movie_id,my_api_key,movie_title,movie_title_org) {
  $.ajax({
    type:'GET',
    url:'https://api.themoviedb.org/3/movie/'+movie_id+'?api_key='+my_api_key,
    success: function(movie_details){
      show_details(movie_details,movie_title,my_api_key,movie_id,movie_title_org);
    },
    error: function(error){
      alert("API Error! - "+error);
      $("#loader").delay(500).fadeOut();
    },
  });
}

// passing all the details to python's flask for displaying and scraping the movie reviews using imdb id
function show_details(movie_details,movie_title,my_api_key,movie_id,movie_title_org){
  var imdb_id = movie_details.imdb_id;
  var poster;
  if(movie_details.poster_path){
    poster = 'https://image.tmdb.org/t/p/original'+movie_details.poster_path;
  }
  else {
    poster = 'static/default.jpg';
  }
  var overview = movie_details.overview;
  var genres = movie_details.genres;
  var rating = movie_details.vote_average;
  var vote_count = movie_details.vote_count;
  var release_date = movie_details.release_date;
  var runtime = parseInt(movie_details.runtime);
  var status = movie_details.status;
  var genre_list = []
  for (var genre in genres){
    genre_list.push(genres[genre].name);
  }
  var my_genre = genre_list.join(", ");
  if(runtime%60==0){
    runtime = Math.floor(runtime/60)+" hour(s)"
  }
  else {
    runtime = Math.floor(runtime/60)+" hour(s) "+(runtime%60)+" min(s)"
  }

  // calling `get_movie_cast` to get the top cast for the queried movie
  movie_cast = get_movie_cast(movie_id,my_api_key);
  
  // calling `get_individual_cast` to get the individual cast details
  ind_cast = get_individual_cast(movie_cast,my_api_key);

  // calling `get_recommendations` to get the recommended movies for the given movie id from the TMDB API
  recommendations = get_recommendations(movie_id, my_api_key);
  
  details = {
      'title':movie_title,
      'cast_ids':JSON.stringify(movie_cast.cast_ids),
      'cast_names':JSON.stringify(movie_cast.cast_names),
      'cast_chars':JSON.stringify(movie_cast.cast_chars),
      'cast_profiles':JSON.stringify(movie_cast.cast_profiles),
      'cast_bdays':JSON.stringify(ind_cast.cast_bdays),
      'cast_bios':JSON.stringify(ind_cast.cast_bios),
      'cast_places':JSON.stringify(ind_cast.cast_places),
      'imdb_id':imdb_id,
      'poster':poster,
      'genres':my_genre,
      'overview':overview,
      'rating':rating,
      'vote_count':vote_count.toLocaleString(),
      'rel_date':release_date,  
      'release_date':new Date(release_date).toDateString().split(' ').slice(1).join(' '),
      'runtime':runtime,
      'status':status,
      'rec_movies':JSON.stringify(recommendations.rec_movies),
      'rec_posters':JSON.stringify(recommendations.rec_posters),
      'rec_movies_org':JSON.stringify(recommendations.rec_movies_org),
      'rec_year':JSON.stringify(recommendations.rec_year),
      'rec_vote':JSON.stringify(recommendations.rec_vote),
      'rec_ids':JSON.stringify(recommendations.rec_ids)
  }

  $.ajax({
    type:'POST',
    data:details,
    url:"/recommend",
    dataType: 'html',
    complete: function(){
      $("#loader").delay(500).fadeOut();
    },
    success: function(response) {
      $('.results').html(response);
      $('#autoComplete').val('');
      $('.footer').css('position','absolute');
      if ($('.movie-content')) {
        $('.movie-content').after('<div class="gototop"><i title="Go to Top" class="fa fa-arrow-up"></i></div>');
      }
      $(window).scrollTop(0);
    }
  });
}

// getting the details of individual cast
function get_individual_cast(movie_cast,my_api_key) {
    cast_bdays = [];
    cast_bios = [];
    cast_places = [];
    for(var cast_id in movie_cast.cast_ids){
      $.ajax({
        type:'GET',
        url:'https://api.themoviedb.org/3/person/'+movie_cast.cast_ids[cast_id]+'?api_key='+my_api_key,
        async:false,
        success: function(cast_details){
          cast_bdays.push((new Date(cast_details.birthday)).toDateString().split(' ').slice(1).join(' '));
          if(cast_details.biography){
            cast_bios.push(cast_details.biography);
          }
          else {
            cast_bios.push("Not Available");
          }
          if(cast_details.place_of_birth){
            cast_places.push(cast_details.place_of_birth);
          }
          else {
            cast_places.push("Not Available");
          }
        }
      });
    }
    return {cast_bdays:cast_bdays,cast_bios:cast_bios,cast_places:cast_places};
  }

// getting the details of the cast for the requested movie
function get_movie_cast(movie_id,my_api_key){
    cast_ids= [];
    cast_names = [];
    cast_chars = [];
    cast_profiles = [];
    top_10 = [0,1,2,3,4,5,6,7,8,9];
    $.ajax({
      type:'GET',
      url:"https://api.themoviedb.org/3/movie/"+movie_id+"/credits?api_key="+my_api_key,
      async:false,
      success: function(my_movie){
        if(my_movie.cast.length>0){
          if(my_movie.cast.length>=10){
            top_cast = [0,1,2,3,4,5,6,7,8,9];
          }
          else {
            top_cast = [0,1,2,3,4];
          }
          for(var my_cast in top_cast){
            cast_ids.push(my_movie.cast[my_cast].id)
            cast_names.push(my_movie.cast[my_cast].name);
            cast_chars.push(my_movie.cast[my_cast].character);
            if(my_movie.cast[my_cast].profile_path){
              cast_profiles.push("https://image.tmdb.org/t/p/original"+my_movie.cast[my_cast].profile_path);
            }
            else {
              cast_profiles.push("static/default.jpg");
            }
          }
        }
      },
      error: function(error){
        alert("Invalid Request! - "+error);
        $("#loader").delay(500).fadeOut();
      }
    });

    return {cast_ids:cast_ids,cast_names:cast_names,cast_chars:cast_chars,cast_profiles:cast_profiles};
  }

  // getting recommendations
  function get_recommendations(movie_id, my_api_key) {
    rec_movies = [];
    rec_posters = [];
    rec_movies_org = [];
    rec_year = [];
    rec_vote = [];
    rec_ids = [];
    
    $.ajax({
      type: 'GET',
      url: "https://api.themoviedb.org/3/movie/"+movie_id+"/recommendations?api_key="+my_api_key,
      async: false,
      success: function(recommend) {
        for(var recs in recommend.results) {
          rec_movies.push(recommend.results[recs].title);
          rec_movies_org.push(recommend.results[recs].original_title);
          rec_year.push(new Date(recommend.results[recs].release_date).getFullYear());
          rec_vote.push(recommend.results[recs].vote_average);
          rec_ids.push(recommend.results[recs].id)
          if(recommend.results[recs].poster_path){
            rec_posters.push("https://image.tmdb.org/t/p/original"+recommend.results[recs].poster_path);
          }
          else {
            rec_posters.push("static/default.jpg");
          }
        }
      },
      error: function(error) {
        alert("Invalid Request! - "+error);
        $("#loader").delay(500).fadeOut();
      }
    });
    return {rec_movies:rec_movies,rec_movies_org:rec_movies_org,rec_posters:rec_posters,rec_year:rec_year,rec_vote:rec_vote,rec_ids:rec_ids};
  }
