// Enforces type
interface sidebarProps {
  fill: string;
}

const Logout = ({ fill }: sidebarProps) => {
  return (
    <svg
      width="24"
      height="25"
      viewBox="0 0 24 25"
      fill={fill}
      xmlns="http://www.w3.org/2000/svg"
    >
      <g id="Logout" clip-path="url(#clip0_33_808)">
        <path
          id="Vector"
          d="M17.9873 8.33333L16.7947 9.50833L18.9769 11.6667H10.3748V13.3333H18.9769L16.7947 15.4833L17.9873 16.6667L22.2165 12.5L17.9873 8.33333ZM6.99147 6.66667H13.7581V5H6.99147C6.06105 5 5.2998 5.75 5.2998 6.66667V18.3333C5.2998 19.25 6.06105 20 6.99147 20H13.7581V18.3333H6.99147V6.66667Z"
          fill={fill}
        />
      </g>
      <defs>
        <clipPath id="clip0_33_808">
          <rect
            width="27.0554"
            height="23.99"
            fill={fill}
            transform="translate(-0.338867)"
          />
        </clipPath>
      </defs>
    </svg>
  );
};

export default Logout;
