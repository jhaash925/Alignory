function SkillsCard({ title, skills, color }) {

  return (

    <div>

      <h3 className={`text-lg font-semibold text-${color}-600 mb-2`}>
        {title}
      </h3>

      <ul className="space-y-1">

        {skills.map((skill, i) => (
          <li key={i}>
            {color === "green" ? "✔" : "✘"} {skill}
          </li>
        ))}

      </ul>

    </div>

  );
}

export default SkillsCard;