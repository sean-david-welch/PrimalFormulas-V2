import utils from '../styles/Utils.module.css';

import { useNavigate } from 'react-router-dom';
import { NavButtonProps } from '../types/miscTypes';

function NavButton({ to, label, icon, onClick }: NavButtonProps) {
	const navigate = useNavigate();

	const handleClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
		if (onClick) {
			onClick(event);
		}
		if (to) {
			navigate(to);
		}
	};

	return (
		<li className={utils.navButton}>
			<button className={utils.btn} onClick={handleClick}>
				{label} <i>{icon}</i>
			</button>
		</li>
	);
}

export default NavButton;
