import "./headers.css"

interface TaglineProps{
    text: string
}

const Tagline = ({text}: TaglineProps) => {
  return (
    <div className="tagline">{text}</div>
  );
};

export default Tagline;
