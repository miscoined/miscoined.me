(in-package :cl-user)
(defpackage miscoined
  (:use :cl)
  (:import-from :miscoined.config
                :config)
  (:import-from :clack
                :clackup)
  (:export :start
           :stop))
(in-package :miscoined)

(defvar *appfile-path*
  (asdf:system-relative-pathname :miscoined #P"app.lisp"))

(defvar *handler* nil)

(defun start (&rest args &key server port debug &allow-other-keys)
  (declare (ignore server port debug))
  (when *handler*
    (restart-case (error "Server is already running.")
      (restart-server ()
        :report "Restart the server"
        (stop))))
  (setq *handler* (apply #'clackup *appfile-path* args)))

(defun stop ()
  (prog1
      (clack:stop *handler*)
    (setq *handler* nil)))
