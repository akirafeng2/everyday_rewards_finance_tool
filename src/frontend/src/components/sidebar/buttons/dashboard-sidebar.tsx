// Enforces type
interface sidebarProps {
  fill: string;
}

const Dashboard = ({ fill }: sidebarProps) => {
  return (
    <svg
      width="24"
      height="25"
      viewBox="0 0 24 25"
      fill={fill}
      xmlns="http://www.w3.org/2000/svg"
    >
      <g id="Bar chart" clipPath="url(#clip0_33_188)">
        <path
          id="Vector"
          d="M5.74365 9.19605H9.12558V18.992H5.74365V9.19605ZM12.0566 4.9978H15.213V18.992H12.0566V4.9978ZM18.3695 12.9945H21.526V18.992H18.3695V12.9945Z"
          fill={fill}
        />
      </g>
      <defs>
        <clipPath id="clip0_33_188">
          <rect
            width="27.0554"
            height="23.99"
            fill={fill}
            transform="translate(0.106934)"
          />
        </clipPath>
      </defs>
    </svg>
  );
};

export default Dashboard;
