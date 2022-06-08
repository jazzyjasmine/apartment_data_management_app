<!DOCTYPE html>
<html lang="en">
<head>
    <title>Search Results</title>
    <style>
        table, th, td {
            border: 1px solid black;
        }
    </style>
</head>
<body>
<div>
    % if apartments:
    <table>
        <tr>
            <th>Apartment Name</th>
            <th>Street Address</th>
            <th>City</th>
            <th>State</th>
            <th>Zipcode</th>
        </tr>

        % for apartment in apartments:
        <tr>
            <td>{{ apartment['apartment_name'] }}</td>
            <td>{{ apartment['street_address'] }}</td>
            <td>{{ apartment['city'] }}</td>
            <td>{{ apartment['state'] }}</td>
            <td>{{ apartment['zipcode'] }}</td>
            <td><a href="/editApartment/{{ apartment['apartment_id'] }}">View/Edit</a></td>
            <td><a href="/deleteApartment/{{ apartment['apartment_id'] }}">Delete</a></td>
            <td><a href="/floorplans/{{ apartment['apartment_id'] }}">Show Floorplans</a></td>
            <td><a href="/addFloorplan/{{ apartment['apartment_id'] }}">Add Floorplan</a></td>
        </tr>
        % end
    </table>
    % else:
    <p>No apartments found.</p>
    % end
</div>
<div>
    <h2>Add a new apartment:</h2>
    <form action="/apartments" method="post">
        <label for="aptName">Apartment Name</label><span style="color:#ff0000">*</span><br>
        <input type="text" id="aptName" name="aptName" required><br>
        <br>
        <label>Laundry Type</label><br>
        <input type="radio" id="onsiteLaundry" name="laundryType" value="1">
        <label for="onsiteLaundry">onsite laundry</label><br>
        <input type="radio" id="inunitLaundry" name="laundryType" value="2">
        <label for="inunitLaundry">in-unit laundry</label><br>
        <input type="radio" id="unknownLaundry" name="laundryType" value="3" checked="checked">
        <label for="unknownLaundry">set to NULL</label><br>
        <br>
        <label>Parking Type</label><br>
        <input type="radio" id="streetParking" name="parkingType" value="1">
        <label for="streetParking">street parking</label><br>
        <input type="radio" id="cityRunParking" name="parkingType" value="2">
        <label for="cityRunParking">city-run parking</label><br>
        <input type="radio" id="apartmentRunParking" name="parkingType" value="3">
        <label for="apartmentRunParking">apartment-run parking</label><br>
        <input type="radio" id="unknownParking" name="parkingType" value="4" checked="checked">
        <label for="unknownParking">set to NULL</label><br>
        <br>
        <label for="landlordID">Landlord ID</label><br>
        Note: Landlord ID must be an integer between 1 and 7.<br>
        <input type="number" id="landlordID" name="landlordID" min="1" max="7"><br>
        <br>
        <label for="officialWebsite">Official Website</label><br>
        <input type="url" placeholder="https://example.com" pattern="https://.*" id="officialWebsite" name="officialWebsite"><br>
        <br>
        <label for="streetAddress">Street Address</label><span style="color:#ff0000">*</span><br>
        <input type="text" id="streetAddress" name="streetAddress" required><br>
        <br>
        <label for="city">City</label><span style="color:#ff0000">*</span><br>
        <input type="text" id="city" name="city" required><br>
        <br>
        <label for="state">State</label><span style="color:#ff0000">*</span><br>
        (e.g. IL)<br>
        <input type="text" id="state" name="state" size="2" required><br>
        <br>
        <label for="zipcode">Zipcode</label><span style="color:#ff0000">*</span><br>
        (e.g. 60615)<br>
        <input type="text" id="zipcode" name="zipcode" size="5" required><br>
        <br>
        <input type="submit" value="Add">
    </form>
    <br>
    <a href="/">Go back to the homepage</a>
</div>
</body>
</html>