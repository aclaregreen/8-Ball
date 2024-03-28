$(document).ready(function() {
    attachEventListeners()
})

function attachEventListeners(){
    var ball = $("circle[fill='WHITE']");
    var svg = $("svg");
    var id = $("#variable_id").text();
    var x;
    var y;
  
    ball.mousedown(function(event) {

        var ballX = parseFloat(ball.attr("cx"));
        var ballY = parseFloat(ball.attr("cy"));

        var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", ballX);
        line.setAttribute("y1", ballY);
        line.setAttribute("x2", ballX);
        line.setAttribute("y2", ballY);
        line.setAttribute("stroke", "cornflowerblue");
        line.setAttribute("stroke-width", "10");

        // Append the line to the SVG container
        svg.append(line);

// Update the line's end point as the mouse moves within the SVG container
        $(document).mousemove(function(event){
            var ballX = parseFloat($("circle[fill='WHITE']").attr("cx"));
            var ballY = parseFloat($("circle[fill='WHITE']").attr("cy"));

            var ballPx = $("circle[fill='WHITE']").offset().left;
            var ballPy = $("circle[fill='WHITE']").offset().top;

            var tablePageX = $("#table").offset().left;

            var r = ballX / (ballPx - tablePageX);
            x = (event.pageX - ballPx) * r + ballX;
            y = (event.pageY - ballPy) * r + ballY;

            var length = Math.sqrt((x - ballX) * (x - ballX) + (y - ballY) * (y - ballY));
            if (length > 500){
                //console.log("X: ", x, "y: ", y);
                var ratio = 500 / length;
                x = ballX + (x - ballX) * ratio;
                y = ballY + (y - ballY) * ratio;
            }

            line.setAttribute("x2", x);
            line.setAttribute("y2", y);

            // Log the mouse coordinates for debugging
        });
        $(document).mouseup(function(event) {
            // Remove the mousemove event listener
            var velx = (ballX - x) * 20;
            var vely = (ballY - y) * 20;
            shoot(velx, vely, id);

            line.remove();
            $(document).off("mousemove");
            $(document).off("mouseup");
            //svg.empty();
        });
    });
}

function shoot(velx, vely, id){
    $.post("shot", {velx:velx, vely:vely, id:id}, display);
}

function display(data, status){
    var newTable = data.split(":,:")
    newTable.forEach(function(item, index) {
        setTimeout(function(){
            displayShot(item)
        }, 10 * (index + 1))
    })
}
function displayShot(frame){
    $('#content').html(frame)
    attachEventListeners()
}