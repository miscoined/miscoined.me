(defsystem "miscoined-test"
  :defsystem-depends-on ("prove-asdf")
  :author "Kelly Stewart"
  :license ""
  :depends-on ("miscoined"
               "prove")
  :components ((:module "tests"
                :components
                ((:test-file "miscoined"))))
  :description "Test system for miscoined"
  :perform (test-op (op c) (symbol-call :prove-asdf :run-test-system c)))
