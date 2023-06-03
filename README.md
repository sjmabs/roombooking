<h1> Room Booking</h1>
<h4>A full stack room booking web app built using Flask, SQLAlchemy and WTForms.</h4>

<h2> Description</h2>
    <p>
        A go to solution for booking out meeting rooms. If you need a simple way for users within your company
        to be able to book a meeting room, this is the app for you. The booking process becomes simple, allows admins
        to approve or decline room requests as well as fully customise the rooms and the related resources available in
        each.
    </p>
<hr>
<h2>Demonstration</h2>

Link to a short video demo I made for cs50: 
https://youtu.be/eQnyr0VyWkE

**TODO I will add a demonstration of the application here. <br>I will include images/videos and a guide on how the application works.**

<hr>

<h2> Installation Instructions</h2>
<ul>
  <li>Clone repo</li>
  <li>Install requirements.txt</li>
  <li>flask run</li>
  <p><em>
     On first run, you will be prompted in your terminal if you would like to import the dummy data or start with a blank database. Either way, 
  you will be able to access the admin console to add/remove users, rooms, resources etc as you wish.
  </em>
  
  ![image](https://github.com/sjmabs/roombooking/assets/70712946/ed538118-f14f-4f70-bdfc-e9b04891b7a6)
  </p>
  <li>Open http://127.0.0.1:5000</li>
</ul>
<p>
  If you opted to include the dummy data you will have the below users created along with their passwords.

    You will have one admin account created:
        m.scott@office.com - manager

    and two basic user accounts:
        d.schrute@office.com - beets
        j.halpert@office.com - pam
  
  Either way, I would recommend creating your own user with the role set to admin. To do this navigate to http://127.0.0.1:5000/admin and log in using the default credentials;
    **admin** for both the username and password.
  Navigate to the <em>User</em> tab and create your user. 
  
  <strong>Make sure you set the role to admin.</strong>
 
  Now you can either continue creating resources and rooms in the admin console or log in to the main interface using the admin account you just created, and do so from there.
</p>

<h3> 
  
<hr>


