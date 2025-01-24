% rebase('base.tpl', title='Register')
    <form action="/register" method="post">
        <label>Username:</label>
        <input type="text" name="username">
        <label>Email:</label>
        <input type="text" name="email">
        <label>Password:</label>
        <input type="password" name="password">
        <input type="submit" value="Register">
    </form>
% end
