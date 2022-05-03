

<!DOCTYPE html>
<html>
<head>
   <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
  <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Work+Sans&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <title></title>
</head>
<body>

</body>
</html>

<body data-new-gr-c-s-check-loaded="14.1043.0" data-gr-ext-installed="">
<div class="banner ">

	<div class="container">
		<div class="bg-white">
		<div class="row ">
		<div class="col-md-12">
          <div class="white-border ">
      <div class="steps-wizard">
        <ul class="steps">
  <li class="past">
  
    <span class="launch">
      <a href="">Register</a>
    </span><i></i>
  </li>
  <li class="present">
    <span class="launch">
     <a href="register.php" class="color-step" style="color: #065464!important;opacity: 1!important;font-weight: 600;"> Login </a>
    </span><i></i>
  </li>
<!--   <li class="future">
    <span>
      <strong>Step 3</strong>
      Blah blah blah.
    </span><i></i>
  </li> -->
</ul>
      </div>
    </div>
    </div>
			<div class="col-md-6">
				<div class="text-center">
					<img src="images/side-img.png" class="logo-signn">
				</div>
			</div>
			<div class="col-md-6">
				<div class="form-padding">
                      
                      <div class="text-center mb-3 mt-3">
                      	<img src="images/emailldpi.png">
                      </div>					
						<div class="text-center">

							<h1 class="login-clr">Check your mail</h1>
						</div>

 
<div class="mt-4">
  <button type="submit" class="btn submit"><a href="reset.php" style="text-decoration: none;color: white;"> VERIFY</a></button>
 
</div>
<div class="text-center mt-2">
	<span>Skip, I'll confirm later</span>
</div>
<div class="text-center mt-4">
	 <p style="font-size: 15px;color:  #313131;">Did not receive the email? Check your spam filter, or  <a href="index.php">Resend</a></p>
</div>

				</div>
			</div>
		</div>
	</div>
</div>
</div>





 <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>



<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/slick.min.js"></script>

<script src="js/comman.js"></script>




<script type="">







	$('.slider').slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  arrows: true,
  dots: false,
  centerMode: true,
  variableWidth: true,
  infinite: true,
  focusOnSelect: true,
  cssEase: 'linear',
  touchMove: true,
  prevArrow:'<button class="slick-prev"> < </button>',
  nextArrow:'<button class="slick-next"> > </button>',
  
          responsive: [                        
              {
                breakpoint: 576,
               settings: {
               centerMode: false,
                 variableWidth: false,
               }
              },
        ]
});

$('.nav-tabs a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
     e.target
     e.relatedTarget
     $('.slider').slick('setPosition');
 });

var imgs = $('.slider img');
imgs.each(function(){
  var item = $(this).closest('.item');
  item.css({
    'background-image': 'url(' + $(this).attr('src') + ')', 
    'background-position': 'center',            
    '-webkit-background-size': 'cover',
    'background-size': 'cover', 
  });
  $(this).hide();
});
</script>







</body>