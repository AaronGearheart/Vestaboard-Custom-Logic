# Vestaboard Custom Logic
Template to create your own custom logic for the Vestaboard Local API

### How to create your owm logic
1: Visit [Vestaboard](https://docs.vestaboard.com/docs/local-api/introduction/) to see documentation on how to get a local API key. <br>
2: Create your own logic for the board using the [template.py](template/template.py) file. Any message you want to send needs to end up in the message variable.
3: Test the template either with your Vestaboard or have it print out the finished data (converted_data variable) and plug it into the [vestaboard_list_to_string.py](/vestaboard_list_to_string.py) file to translate to what the board will look like <br>
4: Deploy custom logic on a local network machine and enjoy! <br>
NOTE: THe exmaple.py was designed first and therefore doesn't actually use the template.py but template.py still works the same aand the example is just a demo of what can be done.

### Example.py Setup
If you want to use the example.py or test it just place your Local API key (from [Vestaboard](https://docs.vestaboard.com/docs/local-api/introduction/)) in a file called VESTABOARD_KEY in the same directory as the script. Now, in the example.py script, set the IP for your Vestaboard (Do not add the :7000 it is added later) and run the script. Typing ADMIN into the time slot will instantly update instead of waiting for the set time.

### Dev_Utils Folder
The [dev_utils](dev_utils/) folder contains useful scripts for development such as a [script](dev_utils/string_to_vestaboard_list.py) to transform (most) strings into a Vestaboard Array and a [script](dev_utils/vestaboard_list_to_string.py) to transform a Vestaboard Array back to a string.

### Contributing
Feel free to fork and make a pull request if you have any changes or issues. Contribution is much appreciated. <br>
Create a pull request if you have an example you would like me to add to the project. 
