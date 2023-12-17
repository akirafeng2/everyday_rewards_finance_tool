interface SubHeaderProps{
    text: string
}

const SubHeader = ({text}: SubHeaderProps) => {
  return (
    <div className="subheader">{text}</div>
  );
};

export default SubHeader;
