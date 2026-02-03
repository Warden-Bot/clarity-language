const { exec } = require('child_process');
const fs = require('fs');

const postId = '18cebeca-6ff4-43d0-b405-8a8c6707d5c7';
const apiKey = 'moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50';
const startTime = Date.now();
const duration = 30 * 60 * 1000; // 30 minutes

function checkPost() {
    const currentTime = Date.now();
    
    if (currentTime - startTime >= duration) {
        console.log('Monitoring period complete.');
        process.exit(0);
        return;
    }

    console.log(`Checking post at ${new Date().toISOString()}`);
    
    const command = `curl.exe -X GET https://www.moltbook.com/api/v1/posts/${postId} -H "Authorization: Bearer ${apiKey}"`;
    
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return;
        }
        
        try {
            const data = JSON.parse(stdout);
            
            if (data.success && data.post) {
                console.log(`Title: ${data.post.title}`);
                console.log(`Upvotes: ${data.post.upvotes}, Downvotes: ${data.post.downvotes}`);
                console.log(`Comments: ${data.post.comment_count}`);
                
                if (data.comments && data.comments.length > 0) {
                    console.log('Recent comments:');
                    data.comments.forEach(comment => {
                        console.log(`- ${comment.author.name}: "${comment.content.substring(0, 60)}..." (${comment.upvotes} upvotes)`);
                    });
                } else {
                    console.log('No comments yet.');
                }
                
                console.log('---');
            } else {
                console.error('Failed to get post data:', data.error);
            }
        } catch (parseError) {
            console.error('Error parsing response:', parseError.message);
        }
    });
}

// Check immediately
checkPost();

// Then check every 2 minutes
setInterval(checkPost, 2 * 60 * 1000);