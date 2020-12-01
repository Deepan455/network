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
		let likes=message.likes;
		button.innerHTML='<img src="/media/liked.svg" class="react"/>'
		button.innerHTML+=likes;
	})
}

function unlike(post,button){
	fetch(`/unlike/${post}`)
	.then(response=>response.json())
	.then(message=>{
		var likes=message.likes;
		button.innerHTML='<img src="/media/not_liked.svg" class="react"/>'
		button.innerHTML+=likes;
	})
}

document.addEventListener('DOMContentLoaded',()=>{
	
	//To follow a user
	followbutton=document.querySelector('.follow')
	if(followbutton){
		followbutton.onclick=()=>{
			let tofollow=document.querySelector('.user_name').innerHTML;
			if(followbutton.dataset.add=='follow'){
				follow(tofollow);
				followbutton.dataset.add="unfollow";
				followbutton.class="follow btn";
				followbutton.innerHTML='Unfollow';
			}
			else
			{
				unfollow(tofollow);
				followbutton.dataset.add="follow";
				followbutton.class="follow btn";
				followbutton.innerHTML='Follow';
			}
		}
	}

	//To like or dislike a post
	document.querySelectorAll('.actions').forEach(button=>{
		button.onclick=()=>{
			let data=button.dataset.press;
			let status=button.dataset.status;
			if(status=="not_liked")
			{	
				console.log("in not liked")
				like(data,button);
				button.dataset.status="liked";
				button.class="actions liked";
			}
			else
			{
				unlike(data,button);
				button.dataset.status="not_liked";
				button.class="actions not_liked";
			}		
		}
	})

	//Link to the post page
	document.querySelectorAll('.post').forEach(post=>{
		let id=post.querySelector('.post_id').innerHTML;
		post.querySelector('.content').onclick=()=>{
			location.href=`/post/${id}`;
		}
	})

	//To display list of followers or following
	click=document.querySelectorAll('.here').forEach(list=>{
		list.onclick=()=>{
			list.querySelector('ul').style.display='block';
		};
	});

})
