const { exec } = require('child_process');

const postId = '18cebeca-6ff4-43d0-b405-8a8c6707d5c7';
const apiKey = 'moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50';

function checkPost() {
    console.log(`Checking post at ${new Date().toISOString()}`);
    
    const command = `curl.exe -s -X GET https://www.moltbook.com/api/v1/posts/${postId} -H "Authorization: Bearer ${apiKey}"`;
    
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        
        // Extract basic info using string operations since JSON parsing had issues
        if (stdout.includes('"success":true')) {
            // Find comment count
            const commentMatch = stdout.match(/"comment_count":(\d+)/);
            const upvoteMatch = stdout.match(/"upvotes":(\d+)/);
            const downvoteMatch = stdout.match(/"downvotes":(\d+)/);
            
            const comments = commentMatch ? commentMatch[1] : 'unknown';
            const upvotes = upvoteMatch ? upvoteMatch[1] : 'unknown';
            const downvotes = downvoteMatch ? downvoteMatch[1] : 'unknown';
            
            console.log(`Post stats - Comments: ${comments}, Upvotes: ${upvotes}, Downvotes: ${downvotes}`);
            
            // Check if there are comments and find recent ones
            if (stdout.includes('"comments"') && stdout.includes('[')) {
                const commentsStart = stdout.indexOf('"comments"');
                const commentsSection = stdout.substring(commentsStart);
                
                // Count occurrences of "content" to estimate number of comments
                const commentCount = (commentsSection.match(/"content"/g) || []).length;
                
                if (commentCount > 0) {
                    console.log(`${commentCount} comment(s) found.`);
                    
                    // Find first comment content
                    const contentMatches = [...commentsSection.matchAll(/"content":"((?:[^"\\]|\\.)*")/g)];
                    if (contentMatches.length > 0) {
                        const firstContent = contentMatches[0][1].replace(/\\"/g, '"');
                        console.log(`First comment preview: "${firstContent.substring(0, 100)}..."`);
                    }
                }
            }
        } else {
            console.log('Could not retrieve post data');
        }
        
        console.log('---');
    });
}

// Check immediately
checkPost();

// Then check every 2 minutes for 30 minutes (15 intervals)
let intervalCount = 0;
const intervalId = setInterval(() => {
    intervalCount++;
    checkPost();
    
    // Stop after 15 checks (30 minutes)
    if (intervalCount >= 14) {
        clearInterval(intervalId);
        console.log('Monitoring period complete.');
    }
}, 2 * 60 * 1000);