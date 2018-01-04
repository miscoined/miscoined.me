(in-package :cl-user)
(defpackage miscoined.web
  (:use :cl
        :caveman2
        :miscoined.config
        :miscoined.view)
  (:export :*web*))
(in-package :miscoined.web)

;; for @route annotation
(syntax:use-syntax :annot)

;;
;; Application

(defclass <web> (<app>) ())
(defvar *web* (make-instance '<web>))
(clear-routing-rules *web*)

;;
;; Routing rules

(defroute "/" ()
  (render "index.html"))

;;
;; Error pages

(defmethod on-exception ((app <web>) (code (eql 404)))
  (declare (ignore app))
  (merge-pathnames #P"_errors/404.html" *template-directory*))
