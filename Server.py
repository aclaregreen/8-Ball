import sys; # used to get argv
 # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import Physics
import math
import os

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/shoot.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith("/table") and parsed.path.endswith(".svg"):
            # this one is different because its an image file
            # retreive the HTML file (binary, not text file)
            try:
                with open(parsed.path[1:]) as file:
                    content = file.read()
                    self.send_response( 200 ); # OK
                        # notice the change in Content-type
                    self.send_header( "Content-type", "image/svg+xml" );
                    self.send_header( "Content-length", len( content ) );
                    self.end_headers();
                    self.wfile.write(bytes(content, "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        if parsed.path in [ '/display.html' ]:
            #receive data
            content_len = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_len).decode('utf-8')
            form_data = dict(parse_qsl(post_data))

            db = Physics.Database( reset=True );
            db.createDB();
            player1 = form_data.get("player1", None)
            player2 = form_data.get("player2", None)
            gameName = form_data.get("gameName", None)
            gameId = form_data.get("gameId", None)

            game = Physics.Game(gameId, gameName, player1, player2)

            for filename in os.listdir("."):
                if filename.startswith("table-") and filename.endswith(".svg"):
                    os.remove(filename)
            table = Physics.Table()

            pos = Physics.Coordinate( 
                    Physics.TABLE_WIDTH / 2.0,
                    Physics.TABLE_WIDTH / 2.0,
                    );

            sb = Physics.StillBall( 1, pos );
            table += sb;

            # 2 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 2, pos );
            table += sb;

            # 3 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            sb = Physics.StillBall( 3, pos );
            table += sb;

            #4 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 -
                            (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 4, pos );
            table += sb;

            #5 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 5, pos );
            table += sb;

            #6 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                            (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 6, pos );
            table += sb;

            #7 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 -
                            (Physics.BALL_DIAMETER+4.0)/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)  -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 7, pos );
            table += sb;

            #8 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)  -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 8, pos );
            table += sb;
            #9 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)  -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 9, pos );
            table += sb;
            #10 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                            (Physics.BALL_DIAMETER+4.0)/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)  -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 10, pos );
            table += sb;
            #11 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 -
                            (Physics.BALL_DIAMETER+4.0)/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 -
                            (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 11, pos );
            table += sb;
            #12 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 -
                            (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 12, pos );
            table += sb;
            #13 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 13, pos );
            table += sb;
            #14 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                            (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 14, pos );
            table += sb;
            #15 ball
            pos = Physics.Coordinate(
                            Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                            (Physics.BALL_DIAMETER+4.0)/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                            (Physics.BALL_DIAMETER+4.0)/2.0,
                            Physics.TABLE_WIDTH/2.0 - 
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) -
                            math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)
                            );
            
            sb = Physics.StillBall( 15, pos );
            table += sb;
            # cue ball also still
            pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0,
                                    Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
            sb  = Physics.StillBall( 0, pos );

            table += sb;

            # pos = Physics.Coordinate(677, 2025)
            
            # sb = Physics.StillBall(0, pos)
            # table += sb
            table_id = db.writeTable(table)
            file = []
            f = open("table.svg", "w")
            f.write(table.svg())
            file.append("table.svg")
            f.close()

            # Read the content of the SVG file
            with open("table.svg", "r") as svg_file:
                svg_content = svg_file.read()
                
            # Open the HTML file in write mode
            with open("display.html", "w") as fptr:
                # Write the HTML content
                fptr.write("<html>\n")
                fptr.write("<head>\n")
                fptr.write("<title>Shoot HTML</title>\n")
                fptr.write("<script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>")
                fptr.write("</head>\n")
                fptr.write("<body>\n")
                fptr.write("<div id='content'>")
                fptr.write("</div>")
                #fptr.write("<svg id='svgContainer' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>\n")
                fptr.write("<svg id='svgContainer' width='700' height='1375' viewBox='-25 -25 1400 2750' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>\n")
                # Include the content of table.svg directly here
                fptr.write(svg_content)

                fptr.write("</svg>\n")

                # Include other HTML content
                fptr.write("<h1>8 Ball</h1>\n")
                fptr.write("<a href='shoot.html'>BACK</a>\n")
                
                # Include JavaScript code
                fptr.write("<script>\n")
                with open("game.js", "r") as js_file:
                    fptr.write(js_file.read())
                fptr.write("</script>\n")

                # Close the body and html tags
                fptr.write("</body>\n")
                fptr.write("</html>\n")

            with open("display.html", "r") as fptr:
                content = fptr.read()

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
        elif parsed.path == '/shot':

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = dict(parse_qsl(post_data))

            # Retrieve 'velx' and 'vely' from form data
            velx = float (form_data.get('velx'))
            vely = float (form_data.get('vely'))

            speed = math.sqrt((velx * velx) + (vely * vely))
            accx = 0
            accy = 0
            if speed > Physics.VEL_EPSILON:
                accx = velx / speed * Physics.DRAG
                accy = vely / speed * Physics.DRAG


            

            print(velx, vely)
            with open("display.html", "w") as fptr:
                # Write the HTML content
                fptr.write("<html>\n")
                fptr.write("<head>\n")
                fptr.write("<title>Shoot HTML</title>\n")
                fptr.write("<script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>")
                fptr.write("</head>\n")
                fptr.write("<body>\n")
                fptr.write("<div id='content'>")
                fptr.write("</div>")
                fptr.write("<p>Shoot</p>")
                #fptr.write("<h1>8 Ball</h1>\n")
                #fptr.write("<a href='display.html'>BACK</a>\n")
                fptr.write("<script>\n")
                with open("game.js", "r") as js_file:
                    fptr.write(js_file.read())
                fptr.write("</script>\n")
                fptr.write("</body>\n")
                fptr.write("</html>\n")

            # Read the updated content of 'display.html'
            with open("display.html", "r") as fptr:
                content = fptr.read()

            # Send the updated content as the response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    print (f"http://localhost:{sys.argv[1]}/shoot.html")
    httpd.serve_forever();
