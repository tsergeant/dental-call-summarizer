import { useState } from "react"

export default function CreateCall() {
	const [transcript, setTranscript] = useState("")
	const [creating, setCreating] = useState(false)
	const [callCreated, setCallCreated] = useState<any>(null)

	const generateTranscript = async () => {
		const res = await fetch("/api/calls/generate-transcript")
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
				<div className="mt-4 p-4 bg-green-100 rounded">
					✅ Call created with ID #{callCreated.call_id}
				</div>
			)}
		</div>
	)
}
