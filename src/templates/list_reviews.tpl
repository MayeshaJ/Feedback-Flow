% rebase('base_logged_in.tpl', title='List Reviews')

<!-- Search Bar -->
<form action="/reviews/search" method="post">
    <h4>Search for any review by topic or username</h4>
    <div>
        <input type="text" name="query" placeholder="Search for any reviews..." required>
        <input type="submit" value="Search">
    </div>
</form>

<h2>Your Reviews</h2>

<!-- Filter Buttons -->
<form action="/reviews" method="post">
    <input type="submit" name="filter" value="all" {{ 'checked' if filter_criteria == 'all' else '' }}> All 
    <input type="submit" name="filter" value="published" {{ 'checked' if filter_criteria == 'published' else '' }}> Published 
    <input type="submit" name="filter" value="draft" {{ 'checked' if filter_criteria == 'draft' else '' }}> Draft
</form>

<!-- List Reviews -->
<ul>
% for review in reviews:
    <li>
        {{review.review_text}}

        <!-- Effort Rating -->
        <p>Effort expended on this topic: {{review.ratings[0]}}/10</p>

        <!-- Communication Rating -->
        <p>Communication with team: {{review.ratings[1]}}/10</p>

        <!-- Participation Rating -->
        <p>Participation in critical reviews: {{review.ratings[2]}}/10</p>

        <!-- Attendance Rating -->
        <p>Attending team meetings: {{review.ratings[3]}}/10</p>

        % if review.status == 'draft':
            <a href="/reviews/{{review.id}}/edit">Edit</a>
        % else:
            <form action="/reviews/{{review.id}}/delete" method="post">
                <button type="submit">Delete</button>
            </form>
        % end
    </li>
% end
</ul>
