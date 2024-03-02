import utils from '../styles/Utils.module.css';

const Loading: React.FC = () => {
    return (
        <div className={utils.spinner}>
            <div className={utils.loadingPage}></div>
        </div>
    );
};

export default Loading;
