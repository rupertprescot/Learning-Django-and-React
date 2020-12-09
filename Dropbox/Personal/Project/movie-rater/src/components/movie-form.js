import React, { useState, useEffect } from 'react';
import API from '../api-service';
import { useCookies } from 'react-cookie';

function MovieForm(props){
	
	const [ title, setTitle ] = useState('');
	const [ description, setDescription ] = useState('');
	const [ createdDate, setcreatedDate ] = useState('');
	const [token] = useCookies(['mr-token']);

	useEffect ( () => {
		setTitle(props.movie.title);
		setDescription(props.movie.description);
		setcreatedDate(props.movie.createdDate);
	}, [props.movie])

	const updateClicked = () => {
		API.updateMovie(props.movie.id, {title, description, createdDate}, token['mr-token'])
		.then( resp => props.updatedMovie(resp))
		.catch( error => console.log(error))
	}

	const createClicked = () => {
		API.createMovie({title, description, createdDate}, token['mr-token'])
		.then( resp => props.movieCreated(resp))
		.catch( error => console.log(error))
	}

	const isDisabled = title.length === 0 || description.length === 0;
	
	return (
		<React.Fragment>
			{ props.movie ? (
				<div>
					<label htmlFor="title">Title</label><br/>
					<input id="title" type="text" placeholder="title" value={title}
						onChange= { evt=> setTitle(evt.target.value)}
					/><br/>
					<label htmlFor="description">Description</label><br/>
					<textarea id="description" type="text" placeholder="description" value={description}
						onChange= { evt=> setDescription(evt.target.value)}
					></textarea><br/>
					<label htmlFor="createdDate">Date</label><br/>
					<input id="createdDate" type="text" placeholder="createdDate" value={createdDate}
						onChange= { evt=> setcreatedDate(evt.target.value)}
					/><br/>
					{ props.movie.id ?
						<button onClick={updateClicked} disabled={isDisabled}>Update</button> : 
						<button onClick={createClicked} disabled={isDisabled}>Create</button>	
					}
					
				</div>
			) : null }
		</React.Fragment>
	)
}

export default MovieForm;