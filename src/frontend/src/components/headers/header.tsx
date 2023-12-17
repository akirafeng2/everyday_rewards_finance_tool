interface HeaderProps{
    text: string
}

const Header = ({text}: HeaderProps) => {
  return (
    <div className="header">{text}</div>
  );
};

export default Header;
