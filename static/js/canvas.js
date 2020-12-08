window.addEventListener("load",()=>{

const canvas = document.querySelector("#canvas");
const ctx = canvas.getContext("2d");
const predictButton = document.querySelector('#btn-predict');
const clearButton = document.querySelector('#btn-clear');
const pen = document.querySelector('#btn-pen');
const eraser = document.querySelector('#btn-eraser');
const prediction_textbox = document.querySelector('#prediction-textbox');
const probability_textbox = document.querySelector('#probability-textbox');
const body = document.querySelector('#body');
var dataURI = '';
var result_correct = null;
var userAns = null;
var pred_value = null;

//Second Box Values
const values_box = document.querySelector('#box_values');
const user_confirm_box = document.querySelector('#user_confirm');
const correct_prediction_box = document.querySelector('#correct_ans');
const incorrect_prediction_box = document.querySelector('#incorrect_ans_que');
const feedback_box = document.querySelector('#feedback_reply');

//User confirm elements
const correct_button = document.querySelector('#btn-correct');
const incorrect_button = document.querySelector('#btn-incorrect');
const dropdown_value = document.querySelector('#digits_dropdown');
const dropdown_submit = document.querySelector('#dropdown_submit');
const draw_again_button = document.querySelector('#btn-draw_again_1');
const draw_again_button2 = document.querySelector('#btn-draw_again_2');

//Initializing the textboxes value
prediction_textbox.value = '';
probability_textbox.value = '';



// Resizing
canvas.height = 200;
canvas.width = 500;


//Setting Background white
ctx.fillStyle = "white";
ctx.fillRect(0,0, canvas.width, canvas.height);



//Getting the Canvas Dimensions
var canvasDimensions = canvas.getBoundingClientRect();
console.log(canvasDimensions.top, canvasDimensions.right, canvasDimensions.bottom, canvasDimensions.left);


//variables
let painting = false;
let start_painting = true;

function startPosition(e){

  if (!start_painting) return;
  painting = true;
  draw(e);
}


function finishedPosition(){
    painting = false;
    ctx.beginPath();
}



function draw(e){


  if(!painting) return;

  // Pen/Eraser shape
  ctx.lineCap = 'round';


//Changing between pen and eraser based on radio button check
  if (pen.checked == true){
    ctx.strokeStyle = "black";
    ctx.lineWidth = 8;

  }else{
    ctx.strokeStyle = "white";
    ctx.lineWidth = 16;

  };
  ctx.lineTo(e.clientX -canvasDimensions.left,e.clientY-canvasDimensions.top);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(e.clientX -canvasDimensions.left,e.clientY-canvasDimensions.top);

}


//Body Function to check if the cursor is withtin the canvas or not

function bodyPosition(e){

  if(e.clientX <= canvasDimensions.left || e.clientX >= canvasDimensions.left + canvas.width || e.clientY <= canvasDimensions.top || e.clientY >= canvasDimensions.top + canvas.height ){
    finishedPosition();
    return;
  };


};

//Function for user confirmation and feedback
function user_feedback(data){

  //Making the values box visible
  values_box.hidden = false;

  //Displaying the predicted Values and its probability
  prediction_textbox.value = data.number;
  probability_textbox.value = data.probability;

  //Making confirmation box visible
  user_confirm_box.hidden = false;
  pred_value =  data.number;




};

//Eventlistener
canvas.addEventListener("mousedown", startPosition);
canvas.addEventListener("mouseup",finishedPosition);
canvas.addEventListener("mousemove",draw);
body.addEventListener("mousemove",bodyPosition);



//Event Triggered on clicking on predict button
predictButton.addEventListener('click', function (e) {

    //Base 64 encoding of the image
    dataURI = canvas.toDataURL("image/png",1);


    ////////Disabling Predict and Clear Button till the probability is displayed after the button is clicked
    predictButton.disabled = true;
    clearButton.disabled = true;
    ctx.disabled = true;
    pen.disabled = true;
    eraser.disabled = true;
  	start_painting = false;

    //Adding the AJAX function to predict the data
    $.ajax({
            type: "GET",
            url: 'ajax/predictnumber/',
            data: {
                "dataURI": dataURI,
            },
            dataType: "json",
            success: function (data) {
                // any process in data

                if (data.status_code == 0){

                //Making the values box unhidden
                  user_feedback(data);


              } else if (data.status_code == 1) {


                alert("Please Draw Something!");
                reset_canvas();

              }


            },
            failure: function () {
                alert("Some error occured while fetching the value. Please Try Again.");
				        draw_again_button.click();

            }


        });


});



function disable_correct_incorrect(){

  correct_button.disabled=true;
  incorrect_button.disabled = true;

};

//Correct button listener
correct_button.addEventListener('click',function(e){

  //Make the correct ans box  visible
  correct_prediction_box.hidden = false;
  disable_correct_incorrect();
  result_correct = true;
  userAns = pred_value;

});


//incorrect button listener
incorrect_button.addEventListener('click',function(e){

  //Ask for the correct ans
  incorrect_prediction_box.hidden = false;
  disable_correct_incorrect();
  result_correct = false;


});

//dropdown submit button
dropdown_submit.addEventListener('click',function(e){

  //Ask for the correct ans
  if(dropdown_value.value == 'none'){
    alert("Please provide the correct value");
  }else{

    console.log("correct ans is " + dropdown_value.value);
    dropdown_submit.disabled = true;
    dropdown_value.disabled = true;
    feedback_box.hidden = false;
    userAns = dropdown_value.value;
  };

});



//Clear Button Functionality
clearButton.addEventListener('click',function(e){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  prediction_textbox.value = '';
  probability_textbox.value = '';

});


//Draw Again Functionality
draw_again_button.addEventListener('click',function(e){


  //Clearing the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  prediction_textbox.value = '';
  probability_textbox.value = '';
  start_painting = true;

  //Enabling all buttons
  predictButton.disabled = false;
  clearButton.disabled = false;
  ctx.disabled = false;
  pen.disabled = false;
  eraser.disabled = false;


  //Clearing and hiding the box 2 elements
  values_box.hidden = true;
  user_confirm_box.hidden = true;
  correct_prediction_box.hidden = true;
  incorrect_prediction_box.hidden = true;
  feedback_box.hidden = true;
  dropdown_value.value = 'none';


  //Enabling box 2 buttons
  correct_button.disabled=false;
  incorrect_button.disabled = false;
  dropdown_submit.disabled = false;





  // To store the prediction data
  //Adding the AJAX function to predict the data
  $.ajax({
          type: "GET",
          url: 'ajax/storedata/',
          data: {
              "values": '{"userAns":'+userAns+',"resultPred":'+ result_correct+'}'
          },
          dataType: "json",
          success: function (data) {
              // any process in data

              if (data.status_code == 0){
                console.log("data inserted successfully");
              } else  {
                alert("Data Not Inserted ");
              };


          },
          failure: function () {
              alert("Some error occured while inserting the data. Please Try Again.");


          }


      });

      //resetting result_correct value
      dataURI = '';
      result_correct = null;
      userAns = null;

});


//Draw Again Functionality
draw_again_button2.addEventListener('click',function(e){


  //Clearing the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  prediction_textbox.value = '';
  probability_textbox.value = '';
  start_painting = true;

  //Enabling all buttons
  predictButton.disabled = false;
  clearButton.disabled = false;
  ctx.disabled = false;
  pen.disabled = false;
  eraser.disabled = false;


  //Clearing and hiding the box 2 elements
  values_box.hidden = true;
  user_confirm_box.hidden = true;
  correct_prediction_box.hidden = true;
  incorrect_prediction_box.hidden = true;
  feedback_box.hidden = true;
  dropdown_value.value = 'none';
  

  //Enabling box 2 buttons
  correct_button.disabled=false;
  incorrect_button.disabled = false;
  dropdown_submit.disabled = false;
  dropdown_value.disabled = false;




  // To store the prediction data
  //Adding the AJAX function to predict the data
  $.ajax({
          type: "GET",
          url: 'ajax/storedata/',
          data: {
              "values": '{"userAns":'+userAns+',"resultPred":'+ result_correct+'}'
          },
          dataType: "json",
          success: function (data) {
              // any process in data

              if (data.status_code == 0){
                console.log("data inserted successfully");
              } else  {
                alert("Data Not Inserted ");
              };


          },
          failure: function () {
              alert("Some error occured while inserting the data. Please Try Again.");
          }


      });

      //resetting result_correct value
      dataURI = '';
      result_correct = null;
      userAns = null;

});


function reset_canvas(){



  //Clearing the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  prediction_textbox.value = '';
  probability_textbox.value = '';
  start_painting = true;


  //Enabling all buttons
  predictButton.disabled = false;
  clearButton.disabled = false;
  ctx.disabled = false;
  pen.disabled = false;
  eraser.disabled = false;


  //Clearing and hiding the box 2 elements
  values_box.hidden = true;
  user_confirm_box.hidden = true;
  correct_prediction_box.hidden = true;
  incorrect_prediction_box.hidden = true;
  feedback_box.hidden = true;
  dropdown_value.value = 'none';


  //Enabling box 2 buttons
  correct_button.disabled=false;
  incorrect_button.disabled = false;
  dropdown_submit.disabled = false;
  dropdown_value.disabled = false;

  //resetting result_correct value
  dataURI = '';
  result_correct = null;
  userAns = null;

};



});
