from flask import Flask, request, render_template
import mbta_helper #Importing the mbta_helper function to this code so it can be used 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place_name = request.form.get("place_name") #the variable place name is retrieved and it is the location submitted by the user on the form
        print(f"Place name received: {place_name}")  # Checking if it has been received correctly. Asked help from ChatGPT because i needed debugging when I kept having a blank page instead of the results

        try:
            # Call the mbta_helper function we defined and imported, with the 2 parameters
            station_name, wheelchair_accessible = mbta_helper.find_stop_near(place_name)
            print(f"Station found: {station_name}, Wheelchair Accessible: {wheelchair_accessible}")  # Debugging

            return render_template(   #Render the template "result" with the variables: city given by the user, the station name, and if it is accessible with wheelchair
                "result.html",
                place_name=place_name,
                station_name=station_name,
                wheelchair_accessible=wheelchair_accessible,)
        
        except Exception as e:
            print(f"Error occurred: {e}")  # Added this because I was able to search for a city but I had a blank page instead of the result
            return render_template("error.html", error_message=str(e))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True) 
