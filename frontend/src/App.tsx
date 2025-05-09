import { useEffect, useState } from 'react'

function App() {
	const [message, setMessage] = useState('...')

	useEffect(() => {
		fetch('http://localhost:8000/hello')
		.then((res) => res.json())
		.then((data) => setMessage(data.message))
		.catch(() => setMessage('Error fetching message'))

	}, [])

	return (
		<div className="p-6 text-center text-xl text-blue-600 font-bold">
			{message}
		</div>
	)
}

export default App
