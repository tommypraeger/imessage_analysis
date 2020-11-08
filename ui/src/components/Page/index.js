import AnalysisPage from './Analysis';
import ContactsPage from './Contacts';
import HomePage from './Home';

const Page = ({ page }) => {
  switch (page) {
    case 'analysis':
      return <AnalysisPage />;

    case 'contacts':
      return <ContactsPage />;

    case 'home':
      return <HomePage />;

    default:
      return <HomePage />;
  }
}

export default Page;
