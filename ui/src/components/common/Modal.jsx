import { useEffect } from "react";
import { createPortal } from "react-dom";

const ensureRoot = () => {
  let el = document.getElementById("modal-root");
  if (!el) {
    el = document.createElement("div");
    el.id = "modal-root";
    document.body.appendChild(el);
  }
  return el;
};

const Modal = ({ isOpen, onRequestClose, children, className = "", overlayClassName = "" }) => {
  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e) => {
      if (e.key === "Escape") onRequestClose?.();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [isOpen, onRequestClose]);

  if (!isOpen) return null;
  const root = ensureRoot();

  const overlayCls = overlayClassName || "fixed inset-0 bg-black/40 z-40";
  const contentCls = className || "fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-5 shadow-lg z-50";

  const content = (
    <div className={overlayCls} onClick={onRequestClose}>
      <div className={contentCls} onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );

  return createPortal(content, root);
};

export default Modal;

