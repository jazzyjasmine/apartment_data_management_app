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
<br>
<a href="/">Go back to the homepage</a>
</body>
</html>