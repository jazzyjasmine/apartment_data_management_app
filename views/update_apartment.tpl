<!DOCTYPE html>
<html lang="en">
<head>
    <title>View or Edit Apartment</title>
    <style>
        table, th, td {
            border: 1px solid black;
        }
    </style>
</head>
<body>
<div>
    <table>
        <tr>
            <th>Apartment ID</th>
            <th>Apartment Name</th>
            <th>Laundry Type</th>
            <th>Parking Type</th>
            <th>Landlord ID</th>
            <th>Landlord Name</th>
            <th>Official Website</th>
            <th>Street Address</th>
            <th>City</th>
            <th>State</th>
            <th>Zipcode</th>
        </tr>

        <tr>
            <td>{{ apartment['apartment_id'] }}</td>
            <td>{{ apartment['apartment_name'] }}</td>
            <td>{{ apartment['laundry_type'] }}</td>
            <td>{{ apartment['parking_type'] }}</td>
            <td>{{ apartment['landlord_id'] }}</td>
            <td>{{ apartment['landlord_name'] }}</td>
            <td>{{ apartment['official_website'] }}</td>
            <td>{{ apartment['street_address'] }}</td>
            <td>{{ apartment['city'] }}</td>
            <td>{{ apartment['state'] }}</td>
            <td>{{ apartment['zipcode'] }}</td>
        </tr>
    </table>
    <br>
    <h2>Update information of this apartment:</h2>
    <form action="/editApartment/{{ apartment['apartment_id'] }}" method="post">
        <label for="aptName">New Apartment Name</label><span style="color:#ff0000">*</span><br>
        <input type="text" id="aptName" name="aptName" value="{{ apartment['apartment_name'] }}" required><br>
        <br>
        <label>New Laundry Type</label><br>
        <input type="radio" id="notChangeLaundry" name="laundryType" value="4" checked="checked">
        <label for="notChangeLaundry">no change</label><br>
        <input type="radio" id="onsiteLaundry" name="laundryType" value="1">
        <label for="onsiteLaundry">onsite laundry</label><br>
        <input type="radio" id="inunitLaundry" name="laundryType" value="2">
        <label for="inunitLaundry">in-unit laundry</label><br>
        <input type="radio" id="unknownLaundry" name="laundryType" value="3">
        <label for="unknownLaundry">set to NULL</label><br>
        <br>
        <label>New Parking Type</label><br>
        <input type="radio" id="notChangeParking" name="parkingType" value="5" checked="checked">
        <label for="notChangeParking">no change</label><br>
        <input type="radio" id="streetParking" name="parkingType" value="1">
        <label for="streetParking">street parking</label><br>
        <input type="radio" id="cityRunParking" name="parkingType" value="2">
        <label for="cityRunParking">city-run parking</label><br>
        <input type="radio" id="apartmentRunParking" name="parkingType" value="3">
        <label for="apartmentRunParking">apartment-run parking</label><br>
        <input type="radio" id="unknownParking" name="parkingType" value="4">
        <label for="unknownParking">set to NULL</label><br>
        <br>
        <input type="submit" value="Update">
    </form>
    <br>
    <a href="/">Go back to the homepage</a>
</div>
</body>
</html>