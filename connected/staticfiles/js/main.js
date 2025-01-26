    let tags = document.getElementsByClassName('project-tag')
	for(let i=0; i<tags.length;i++)
	{
		tags[i].addEventListener('click', (e) => {
			let tagid = e.target.dataset.tagid
			let projectid= e.target.dataset.projectid
			
			fetch('http://127.0.0.1:8004/api/remove-tag/', {
				method:'DELETE',
				headers: {
					'Content-Type':'application/json'
				},

				body: JSON.stringify({'project':projectid, 'tag':tagid})

			})
			.then(resp => resp.json())
			.then(data => {
				e.target.remove()
			})

		})
	}
