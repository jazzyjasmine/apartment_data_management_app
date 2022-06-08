<!DOCTYPE html>
<html lang="en">
<head>
    <title>Floor plans</title>
    <style>
        table, th, td {
            border: 1px solid black;
        }
    </style>
</head>
<body>
<div>
    <h2>Current floor plans</h2>
    % if floorplans:
    <table>
        <tr>
            <th>Apartment ID</th>
            <th>Floor Plan Type</th>
            <th>Floor Plan Area(sqr ft)</th>
            <th>Price Per Month($)</th>
            <th>Leasing Period(month)</th>
        </tr>

        % for floorplan in floorplans:
        <tr>
            <td>{{ floorplan['apartment_id'] }}</td>
            <td>{{ floorplan['floor_plan_type'] }}</td>
            <td>{{ floorplan['floor_plan_area'] }}</td>
            <td>{{ floorplan['price'] }}</td>
            <td>{{ floorplan['leasing_period'] }}</td>
        </tr>
        % end
    </table>
    % else:
    <p>No floor plans found for this apartment.</p>
    % end
</div>
<div>
    <h2>Add a floor plan for this apartment</h2>
    <form action="/addFloorplan/{{ apartment_id }}" method="post">
        <label>Floor Plan Type</label><span style="color:#ff0000">*</span><br>
        <input type="radio" id="studio" name="floorPlanType" value="1" checked="checked">
        <label for="studio">studio</label><br>
        <input type="radio" id="1b1b" name="floorPlanType" value="2">
        <label for="1b1b">1b1b</label><br>
        <input type="radio" id="2b2b" name="floorPlanType" value="3">
        <label for="2b2b">2b2b</label><br>
        <input type="radio" id="2b1b" name="floorPlanType" value="4">
        <label for="2b1b">2b1b</label><br>
        <input type="radio" id="3b2b" name="floorPlanType" value="5">
        <label for="3b2b">3b2b</label><br>
        <br>
        <label for="floorPlanArea">Floor Plan Area(sqr ft)</label><br>
        Note: Floor plan area must be an integer. Leave this field blank if it is NULL.<br>
        <input type="number" id="floorPlanArea" name="floorPlanArea" min="0"><br>
        <br>
        <label for="price">Price Per Month($)</label><span style="color:#ff0000">*</span><br>
        <input type="number" id="price" name="price" min="0" required><br>
        <br>
        <label for="leasingPeriod">Leasing Period(month)</label><span style="color:#ff0000">*</span><br>
        <input type="number" id="leasingPeriod" name="leasingPeriod" min="0" required><br>
        <br>
        <input type="submit" value="Update">
    </form>
    <br>
    <a href="/">Go back to the homepage</a>
</div>
</body>
</html>