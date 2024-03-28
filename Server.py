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

        elif parsed.path in ["/display.css"]:
            fp = open("."+ self.path)
            content = fp.read()
            self.send_response(200)
            self.send_header( "Content-type", "text/css" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();
            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
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

            player1 = form_data.get("player1", None)
            player2 = form_data.get("player2", None)
            gameName = form_data.get("gameName", None)
            gameId = form_data.get("gameId", None)
            if (gameId is not None):
                gameId = int(gameId)

            game = Physics.Game(gameId, gameName, player1, player2)
            id = game.gameID

            for filename in os.listdir("."):
                if filename.startswith("table-") and filename.endswith(".svg"):
                    os.remove(filename)

            # Read the content of the SVG file
            with open("table.svg", "r") as svg_file:
                svg_content = svg_file.read()
                
            # Open the HTML file in write mode
            with open("display.html", "w") as fptr:
                # Write the HTML content
                fptr.write("<html>\n")
                fptr.write("<head>\n")
                fptr.write("<title>Shoot HTML</title>\n")
                fptr.write("<link rel='stylesheet' type='text/css' href='display.css'>")
                fptr.write("<script src='https://code.jquery.com/jquery-3.6.0.min.js'></script>")
                fptr.write("</head>\n")
                fptr.write("<body>\n")
                fptr.write("<h1>8 Ball</h1>\n")
                #fptr.write("<p> Game Id: </p>" + "<p id='variable_id'>{}</p>".format(id))
                fptr.write("<span>Game Id: </span>" + "<span id='variable_id'>{}</span><br>\n".format(id))
                #fptr.write("<p id='variable_id'>{}</p>\n".format(id))
                fptr.write("<a href='shoot.html'>BACK</a>\n")
                fptr.write("<div id='content'>")
                # fptr.write("</div>")
                # fptr.write("<p id='variable_id'>Game ID: {}</p>\n".format(id))
                # fptr.write("<a href='shoot.html'>BACK</a>\n")
                #fptr.write("<svg id='svgContainer' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>\n")
                #fptr.write("<svg id='svgContainer' width='700' height='1375' viewBox='-25 -25 1400 2750' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>\n")
                # Include the content of table.svg directly here
                fptr.write(svg_content)

                fptr.write("</svg>\n")

                fptr.write("</div>")
                # Include other HTML content
                #fptr.write("<h1>8 Ball</h1>\n")
                
                
                
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

            id = int (form_data.get('id'))

            game = Physics.Game(id)
            print("THE TABLE ID IS: ", game.tableID)
            table = game.database.readTable(game.tableID)
            files = game.shoot(game.gameName, game.player1Name, table, velx, vely)
            for i in range(len(files)):
                string = files[i].svg()
                files[i] = string
            content = ":,:".join(files)
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
