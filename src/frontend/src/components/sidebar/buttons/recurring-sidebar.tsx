// Enforces type
interface sidebarProps {
  fill: string;
}

const Recurring = ({ fill }: sidebarProps) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="27"
      height="24"
      viewBox="0 0 27 24"
      fill={fill}
    >
      <g id="Repeat" clipPath="url(#clip0_33_746)">
        <path
          id="Vector"
          d="M8.5522 6.99718H19.8253V9.99593L24.3345 5.9976L19.8253 1.99927V4.99802H6.29758V10.9955H8.5522V6.99718ZM19.8253 16.993H8.5522V13.9943L4.04297 17.9926L8.5522 21.9909V18.9922H22.0799V12.9947H19.8253V16.993Z"
          fill={fill}
        />
      </g>
      <defs>
        <clipPath id="clip0_33_746">
          <rect
            width="27.0554"
            height="23.99"
            fill={fill}
            transform="translate(0.661133)"
          />
        </clipPath>
      </defs>
    </svg>
  );
};

export default Recurring;
