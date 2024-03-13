import "./CalendarBubble.css";
import CalenderIcon from "./components/CalenderIcon";

interface CalendarBubbleInterface {
  children: string;
}

const CalendarBubble = ({ children }: CalendarBubbleInterface) => {
  return (
    <div className="calendarBubble">
      <CalenderIcon />
      <span className="padding"></span>
      <span className="calendarBubbleText">{children}</span>
    </div>
  );
};

export default CalendarBubble;
