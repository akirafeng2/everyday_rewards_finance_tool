interface EmojiProps {
    label: string;
    symbol: string;
}

const Emoji = ({ label, symbol }: EmojiProps)=> (
    <span
        className="emoji"
        role="img"
        aria-label={label ? label : ""}
        aria-hidden={label ? "false" : "true"}
    >
        {symbol}
    </span>
);
export default Emoji;