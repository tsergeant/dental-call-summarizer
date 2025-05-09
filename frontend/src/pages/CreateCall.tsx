import { useState } from "react"

export default function CreateCall() {
	const [transcript, setTranscript] = useState("")
	const [creating, setCreating] = useState(false)
	const [callCreated, setCallCreated] = useState<any>(null)

	const generateTranscript = async () => {
		const res = await fetch("/api/calls/generate-transcript", {
			method: "GET",
			cache: "no-store",
		})
		console.log("Status: ", res.status)
		const data = await res.json()
		setTranscript(data.transcript)
		setCallCreated(null)
	}

	const createCall = async () => {
		if (!transcript) return
		setCreating(true)

		const res = await fetch("/api/calls/", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				phone_number: extractPhone(transcript),
				transcription_text: transcript,
				direction: extractDirection(transcript),
				office_person: extractOfficePerson(transcript),
			}),
		})

		const data = await res.json()
		setCallCreated(data)
		setCreating(false)
	}

	// helper functions
	const extractPhone = (text: string) => {
		const match = text.match(/Metadata: .*?(\d{10})/)
		return match ? match[1] : "5550000000"
	}

	const extractDirection = (text: string) => {
		const match = text.match(/Metadata: .*?;\s*(Incoming|Outgoing)/i)
		return match ? match[1].toLowerCase() : "incoming"
	}

	const extractOfficePerson = (text: string) => {
		const match = text.match(/Metadata: .*?;\s*(?:Incoming|Outgoing);\s*\d{10};\s*(.+)/)
		return match ? match[1].trim() : null
	}

	return (

		<div className="p-4 space-y-4">
		<h2 className="text-xl font-semibold text-gray-800 mb-2">Notes</h2>

		<ul className="list-disc list-inside pl-4">
			<li>
				This page is used to populate the database with call data.
			</li>
			<li>
				Click the <strong>Generate Transcript</strong> button to receive an AI-generated ficticious transcript.
			</li>
			<li>
				Once a transcript is generated, you can click the <strong>Create Call</strong> button to create a call with a summary in the database.
			</li>
			<li>
				If you want to add another call to the database, click the <strong>Generate Transcript</strong> button again to generate a new transcript and then click the <strong>Create Call</strong> button again.	
			</li>
			<li>
				One interesting hidden feature on this page is that if the phone number corresponds to the phone number of a customer, it utilizes a trigger to connect the call with the corresponding entry in the customer table.
			</li>
			<li>
				Use the menu at the top to see the CommLog page and the About page.
			</li>
			<li>
				Not a lot of error handling on this page!
			</li>
		</ul>
		
			<h2 className="text-xl font-bold">Create Call</h2>

			<div className="space-x-2">
				<button
					className="bg-blue-500 text-white px-4 py-2 rounded"
					onClick={generateTranscript}
				>
					Generate Transcript
				</button>
				<button
					className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
					onClick={createCall}
					disabled={!transcript || creating}
				>
					Create Call
				</button>
			</div>

			{transcript && (
				<div className="mt-4 whitespace-pre-wrap bg-gray-100 p-4 rounded">
					{transcript}
				</div>
			)}

			{callCreated && (
				<div className="mt-4 p-4 bg-green-100 border border-green-300 rounded text-green-800">
					<p className="font-semibold mb-2">Call created successfully!</p>
					<p><strong>Summary:</strong></p>
					<p className="whitespace-pre-wrap">{callCreated.summary_text}</p>
				</div>
			)}

		</div>
	)
}
