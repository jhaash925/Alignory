function ATSScore({ score }) {

  return (

    <div className="mb-6">

      <h2 className="text-xl font-semibold mb-2">
        ATS Score
      </h2>

      <div className="w-full bg-gray-200 h-6 rounded">

        <div
          className="bg-green-500 h-6 rounded text-white text-center"
          style={{ width: `${score}%` }}
        >
          {score}%
        </div>

      </div>

    </div>

  );
}

export default ATSScore;