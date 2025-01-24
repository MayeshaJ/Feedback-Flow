% rebase('base_logged_in.tpl', title='List Topics')

<h2>All Topics</h2>
<ul>
% for topic in topics:
    <li>
        {{topic.name}}: {{topic.description}}
        <a href='/topics/{{topic.id}}/create_review'>Create Review</a>
        <ul>
            % for review in reviews.get(topic.id, []):
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
                </li>
            % end
        </ul>
    </li>
% end
</ul>