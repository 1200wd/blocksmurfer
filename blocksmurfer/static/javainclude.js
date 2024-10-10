async function copyContent(id)
{
    let text = document.getElementById(id).innerText
    try {
        await navigator.clipboard.writeText(text);
        console.log('Content copied to clipboard: ', id);
    } catch (err) {
        console.error('Failed to copy: ', err);
    }
}

async function copyContentTitle(id)
{
    let text = document.getElementById(id).title;
    try {
        await navigator.clipboard.writeText(text);
        console.log('Content copied to clipboard: ', id);
    } catch (err) {
        console.error('Failed to copy: ', err);
    }
}
