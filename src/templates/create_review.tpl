% rebase('base_logged_in.tpl', title='Create Review')

<h2>Create Review for Topic ID: {{topic_id}}</h2>
<form action="/topics/{{topic_id}}/create_review" method="post">
    <label for="review_text">Review:</label>
    <textarea id="review_text" name="review_text" rows="4" cols="50" required></textarea>
    <div>
        Rate the following on a scale from 1 to 10:  <br><br>
        <input type="number" name="effort" min="1" max="10"> Effort expended on this topic.   <br>
        <input type="number" name="communication" min="1" max="10"> Communication with team.   <br>
        <input type="number" name="participation" min="1" max="10"> Participation in critical reviews.   <br>
        <input type="number" name="attendance" min="1" max="10"> Attending team meetings.   <br>
    </div>
    <input type="submit" name="save" value="Save Draft">
    <input type="submit" name="publish" value="Publish Review">
</form>
