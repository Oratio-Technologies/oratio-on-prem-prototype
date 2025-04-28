import Logger from '../utils/logger';

interface ButtonProps {
  onClick: () => void;
  label: string;
  // ... other props
}

export const Button = ({ onClick, label, ...props }: ButtonProps) => {
  const handleClick = () => {
    Logger.info('Button Clicked', { label });
    onClick();
  };

  return (
    <button onClick={handleClick} {...props}>
      {label}
    </button>
  );
};
