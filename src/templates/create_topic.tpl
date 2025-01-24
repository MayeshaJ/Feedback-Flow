% rebase('base_logged_in.tpl', title='Create Topic')

<form action="/topics/create" method="post">
    <div>
        <label for="name">Topic Name:</label>
        <input type="text" id="name" name="name" required>
    </div>
    <div>
        <label for="description">Description:</label>
        <textarea id="description" name="description" rows="4" cols="50" required></textarea>
    </div>
    <div>
        <input type="submit" value="Create Topic">
    </div>
</form>