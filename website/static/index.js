console.log("Hello Sadique")
function deleteNote(noteId){
    console.log("Note id"+noteId)
    fetch("/delete-note",{
        method:"POST",
        body:JSON.stringify({noteId:noteId}),
    }).then((_res)=>{
        window.location.href="/";
    });
}