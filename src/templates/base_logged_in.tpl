<!DOCTYPE html>
<html>
    <head>
        <title>{{title or 'Default Title'}}</title>
        <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
        <div class="navbar">
            <a href="/dashboard">Dashboard</a>
            <a href="/topics/add">Create Topic</a>
            <a href="/topics">All Topics</a>
            <a href="/reviews">My Reviews</a>
            <a href="/logout">Logout</a>
        </div>
        {{!base}}
    </body>
</html>