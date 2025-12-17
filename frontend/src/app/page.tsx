import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-white to-gray-100">
      <div className="z-10 max-w-5xl w-full items-center justify-center space-y-8">
        <h1 className="text-6xl font-bold text-center mb-4 text-gray-900">
          Todo App
        </h1>
        <p className="text-center text-xl text-gray-600 mb-12">
          Full-stack multi-user task management application
        </p>

        <div className="flex gap-4 items-center justify-center">
          <Link
            href="/login"
            className="px-8 py-3 bg-teal-500 text-white font-semibold rounded-lg hover:bg-teal-600 transition-colors shadow-md"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="px-8 py-3 bg-white text-teal-500 font-semibold rounded-lg border-2 border-teal-500 hover:bg-teal-50 transition-colors shadow-md"
          >
            Register
          </Link>
        </div>

        <div className="mt-16 text-center text-sm text-gray-500">
          <p>✨ Organize your tasks with priorities, categories, and due dates</p>
          <p className="mt-2">🎯 Beautiful, modern UI with smooth animations</p>
        </div>
      </div>
    </main>
  )
}
