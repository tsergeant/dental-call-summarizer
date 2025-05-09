export default function About() {
    return (
        <div className="p-6 max-w-3xl mx-auto">
            <h1 className="text-2xl font-bold mb-4">About This Project</h1>
            <p className="mb-4">
                This dental office call management application is a toy project to demonstrate full-stack
                web development with AI integration.
            </p>
            <ul className="list-disc list-inside mb-4">
                <li><strong>Frontend:</strong> React + TypeScript + Tailwind CSS</li>
                <li><strong>Backend:</strong> FastAPI + SQLAlchemy</li>
                <li><strong>Database:</strong> PostgreSQL (via Docker)</li>
                <li><strong>AI Integration:</strong> OpenAI's Chat API (for transcript summaries and generation)</li>
                <li><strong>Hosting:</strong> AWS EC2 using Docker Compose</li>
            </ul>
            <p className="bg-blue-50 text-center border border-blue-200 rounded p-4">
                <strong>Terry Sergeant</strong>.  <br />
                <code>terry@gmail.com</code><br />
                <code>325-660-7802</code><br />
                <a href="https://github.com/tsergeant/dental-call-summarizer" target="_blank">github.com/tsergeant/dental-call-summarizer</a>
            </p>
        </div>
    )
}
