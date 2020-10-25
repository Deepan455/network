function follow(user){
	fetch(`/follow/${user}`)
	.then(response=>response.json())
	.then(message=>{
		alert(message.message);
	})
}

function unfollow(user){
	fetch(`/unfollow/${user}`)
	.then(response=>response.json())
	.then(message=>{
		alert(message.message);
	})
}

function like(post,button){
	fetch(`/like/${post}`)
	.then(response=>response.json())
	.then(message=>{
		alert(message.likes);
		let likes=message.likes;
		console.log(likes);
		button.innerHTML=likes;
	})
}

function unlike(post,button){
	fetch(`/unlike/${post}`)
	.then(response=>response.json())
	.then(message=>{
		alert(message.likes);
		var likes=message.likes;
		console.log(likes);
		button.innerHTML=likes;
	})
}

document.addEventListener('DOMContentLoaded',()=>{
	followbutton=document.querySelector('.follow')
	if(followbutton){
		followbutton.onclick=()=>{
			let tofollow=document.querySelector('.user_name').innerHTML;
			if(followbutton.dataset.add=='follow'){
				follow(tofollow);
				followbutton.dataset.add="unfollow";
				followbutton.innerHTML='Unfollow';
			}
			else
			{
				unfollow(tofollow);
				followbutton.dataset.add="follow";
				followbutton.innerHTML='Follow';
			}
		}
	}

	document.querySelectorAll('.actions').forEach(button=>{
		button.onclick=()=>{
			let data=button.dataset.press;
			let status=button.dataset.status;
			console.log(status)
			if(status=="not_liked")
			{	
				console.log("in not liked")
				like(data,button);
				button.dataset.status="liked";
				button.id='liked';
			}
			else
			{
				console.log("in liked");
				unlike(data,button);
				button.dataset.status="not_liked";
				button.id="not_liked";
			}		
		}
	})
})